const _NODE_SEGS=['level','no','shardStart','shardEnd','type','slaves'];
export default {
inject:['service', 'tags'],
data() {return {
    nodes:{}, //[{show:false,list:[]}...]
    newAddr:'',
    dbTypes:['SQLITE','MYSQL','POSTGRE','SQLSERVER','ORACLE','JDBC'],
    node:{dlg:false, idx:0, addr:'', level:0, no:'', shardStart:0, shardEnd:32768, type:"SQLITE", slaves:[]}
}},
created() {
    this.query();
},
methods:{
query() {
    var url="/db/listConfig";
    this.service.request_private({method:"GET",url:url}, "bios").then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        var nodes={};
        var noList=[];
        var oldNodes=this.nodes;
        for(var i of resp.data.list) {
            var addr=i.name; //name(addr)->cfg([{no:xx,level:xxx...},...])
            var list=JSON.parse(i.val);
            for(var l of list) {
                noList.push(parseInt(l.no));
                l.status='N';
            }
            var old=oldNodes[i.name];
            var show=old&&old.show;
            nodes[addr]={show:show, list:list};
        }
        this.query_status(noList.join(','), nodes); //请求status成功后再更新，防止界面刷新时状态错误
    })
},
query_status(noList, nodes) {
    var opts={method:"GET",url:"/status/dbstatus?list="+noList};
    this.service.request_private(opts, "bios").then(resp=>{
        if(resp.code != RetCode.OK) {
            this.nodes=nodes;
            console.warn("query_status failed:" + resp.code + ",info:" + resp.info);
            return;
        }
        for(var i of resp.data.list) {//[{dbNo:xx,partId:xx,shardStart:xx...},...]
            var node=nodes[i.addr];//[{no:xx,partId:xx,shardStart:xx...},...]
            if(!node) continue;
            for(var n of node.list) {
                if(n.no!=i.dbNo||n.shardStart!=i.shardStart) {
                    continue;
                }
                n.status=i.status;
                n.partId=i.partId;
                n.ver=i.ver;
                if(i.status=='Y') {
                    n.cls='text-accent';
                    n.status=this.tags.running;
                }
            }
        }
        this.nodes=nodes;
    })
},
add_server(){
    var opts={method:"put",url:"/db/setConfig", data:{addr:this.newAddr,cfg:"[]"}};
    this.service.request_private(opts, "bios").then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        this.newAddr='';
        this.query();
    })
},
remove_server(addr) {
    var node=this.nodes[addr];
    if(!node) return;
    this.$refs.confirmDlg.show(this.tags.om.cfmRmvSrv, ()=>{
        var opts={method:"DELETE",url:"/db/removeServer?addr="+addr};
        this.service.request_private(opts, "bios").then(resp=>{
            if(resp.code != RetCode.OK) {
                this.$refs.errDlg.showErr(resp.code, resp.info);
                return;
            }
            delete this.nodes[addr];
        })
    })
},
set_node(addr){
    var node=this.nodes[addr];
    if(!node) return;
    var cfg=[];
    for(var l of node.list) {
        cfg.push(copyObj(l, _NODE_SEGS));
    }
    var opts={method:"put",url:"/db/setConfig",data:{addr:addr, cfg:JSON.stringify(cfg)}};
    this.service.request_private(opts, "bios").then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query();
        this.node.dlg=false;
    })
},
show_edit(addr, i) {
    var node=this.nodes[addr];
    if(!node) return;
    copyObjTo(node.list[i], this.node, _NODE_SEGS);
    this.node.dlg=true;
    this.node.idx=i;
    this.node.addr=addr;
},
show_add(addr) {
    this.node={dlg:true, idx:-1, addr:addr, level:0,no:'',shardStart:0,shardEnd:32767,type:"SQLITE",slaves:""};
},
check_node(n) {
    var omTags=this.tags.om;
    if(isNaN(parseInt(n.no))) {
        this.$refs.errDlg.showErr(RetCode.WRONG_PARAMETER, 'invalid '+omTags.dbNo);
        return false;
    }
    if(isNaN(parseInt(n.shardStart)) || n.shardStart<0
       || isNaN(parseInt(n.shardEnd)) || n.shardEnd>32767) {
        this.$refs.errDlg.showErr(RetCode.WRONG_PARAMETER, 'invalid '+omTags.shardStart+' or '+omTags.shardEnd);
        return false;
    }
    if(n.shartStart>=n.startEnd) {
        this.$refs.errDlg.showErr(RetCode.WRONG_PARAMETER, omTags.shardStart+'>='+omTags.shardEnd);
        return false;
    }
    return true;
},
confirm_add() {
    var node=this.nodes[this.node.addr];
    if(!node) return;
    if(!this.check_node(this.node)) return;
    var newNode=copyObj(this.node, _NODE_SEGS);
    node.list.push(newNode);
    this.set_node(this.node.addr);
},
confirm_edit() {
    var node=this.nodes[this.node.addr];
    if(!node||this.node.idx<0) return;
    if(!this.check_node(this.node)) return;
    copyObjTo(this.node, node.list[this.node.idx], _NODE_SEGS);
    this.set_node(this.node.addr);
},
remove_node() {
    var node=this.nodes[this.node.addr];
    if(!node) return;
    this.$refs.confirmDlg.show(this.tags.om.cfmRmvDbNode, ()=>{
        node.list.splice(this.node.idx, 1);
        this.set_node(this.node.addr);
    })
},
check() {
    var opts={method:"get",url:"/db/checkConfig"};
    this.service.request_private(opts, "bios").then(resp=>{
        this.$refs.errDlg.showErr(resp.code, resp.info);
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary">
    <q-toolbar>
      <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
      <q-toolbar-title>{{tags.om.dbNodes}}</q-toolbar-title>
      <q-btn flat dense icon="beenhere" @click="check" color="purple"></q-btn>
    </q-toolbar>
  </q-header>

  <q-page-container>
    <q-page class="q-pa-md">
<div v-for="(n,addr) in nodes" class="q-pa-sm">
 <q-banner class="bg-grey-1" inline-actions dense @click="n.show=!n.show">{{addr}}
  <template v-slot:action>
    <q-btn flat color="primary" icon="delete" dense @click="remove_server(addr)"></q-btn>
    <q-btn flat color="primary" icon="add" dense @click="show_add(addr)"></q-btn>
  </template>
 </q-banner>
 <q-list separator dense v-show="n.show">
  <q-item v-for="(c,i) in n.list" :class="c.cls" clickable @click="show_edit(addr,i)">
   <q-item-section>
    <q-item-label>{{c.no}}({{tags.om.status}}:{{c.status}})</q-item-label>
    <q-item-label caption>{{tags.om.level}}:{{c.level}}</q-item-label>
    <q-item-label caption>{{tags.om.partId}}:{{c.partId}}</q-item-label>
   </q-item-section>
   <q-item-section>
    <q-item-label caption>{{tags.om.mode}}:{{c.type}}-{{c.mode}}</q-item-label>
    <q-item-label caption>{{tags.om.slaves}}:{{c.slaves}}</q-item-label>
    <q-item-label caption>{{tags.om.sharding}}:{{c.shardStart}}-{{c.shardEnd}}</q-item-label>
   </q-item-section>
  </q-item>
 </q-list>
</div>
<div class="q-pa-sm">
 <q-banner class="bg-grey-1" inline-actions dense>
  <q-input v-model="newAddr" dense></q-input>
  <template v-slot:action>
   <q-btn flat color="primary" icon="add" @click="add_server" dense></q-btn>
  </template>
 </q-banner>
</div>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="node.dlg" persistent>
 <q-card style="min-width:62vw;">
  <q-card-section class="row items-center">
   <q-list dense>
    <q-item><q-item-section>
     <q-item-label><q-input dense v-model.number="node.no" :label="tags.om.dbNo"></q-input></q-item-label>
     <q-item-label><q-select v-model="node.dbType" options="dbTypes" label="tags.om.dbType"></q-select></q-item-label>
    </q-item-section></q-item>
    <q-item><q-item-section>
     <q-input dense v-model.number="node.level" :label="tags.om.level"></q-input>
    </q-item-section></q-item>
    <q-item><q-item-section>
     <q-input dense v-model="node.slaves" :label="tags.om.slaves"></q-input>
    </q-item-section></q-item>
    <q-item><q-item-section>
     <q-input dense v-model.number="node.shardStart" :label="tags.om.shardStart"></q-input>
    </q-item-section></q-item>
    <q-item><q-item-section>
     <q-input dense v-model.number="node.shardEnd" :label="tags.om.shardEnd"></q-input>
    </q-item-section></q-item>
   </q-list>
  </q-card-section>

  <q-card-actions align="right">
    <q-btn flat :label="tags.cancel" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="confirm_add" v-if="node.idx<0" dense></q-btn>
    <div v-else>
     <q-btn flat :label="tags.remove" color="primary" @click="remove_node" dense></q-btn>
     <q-btn :label="tags.ok" color="primary" @click="confirm_edit" dense></q-btn>
    </div>
  </q-card-actions>
 </q-card>
</q-dialog>
<component-confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></component-confirm-dialog>
<component-alert-dialog ref="errDlg" :title="tags.failToCall" :close="tags.close"></component-alert-dialog>
`
}