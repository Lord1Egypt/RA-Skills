export default {
inject:['service', 'tags'],
data() {return {
    gid:-1,
    members:[],
    grps:[],
    errMsgs:{},
    newMbr:{dlg:false,uid:[],title:'',role:'NOR'},
    newGrp:{dlg:false,name:'',type:'',descr:'',admin:''},
    edtGrp:{dlg:false,id:0,name:'',descr:''},
    paths:[],
    roleOpts:[]
}},
created(){
    this.open_grp(0, '');
    for(var r in this.tags.roleTp) {
        this.roleOpts.push({value:r, label:this.tags.roleTp[r]});
    }
},
methods:{
query_subs(){//查询子群组及成员
    var opts={method:"GET", url:"/grp/listAll?gid="+this.gid}
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }

        var dt=new Date();
        if(resp.data.members) {
            this.members=resp.data.members.map(m=>{
                dt.setTime(m.update_time);
                m.role=this.tags.roleTp[m.role];
                m.createAt=date2str(dt);
                return m;
            });
        } else {
            this.members=[];
        }
        
        if(resp.data.grps) {
            this.grps=resp.data.grps.map(g=>{
                dt.setTime(g.update_time);
                g.createAt=date2str(dt);
                return g;
            });
        } else {
            this.grps=[];
        }
    })  
},
create_grp() {
    var g=this.newGrp;
    var dta={fid:this.gid, name:g.name,type:g.type, descr:g.descr};
    var opts={method:"POST",url:"/grp/create",data:dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var dt=new Date();
        this.grps.push({id:resp.data.gid,
            name:g.name,type:g.type,descr:g.descr,
            createAt:dt.toLocaleDateString()});
        this.newGrp={dlg:false,name:'',descr:'',type:''};
    });
},
rmv_grp(id,i) {
    var opts={method:"DELETE",url:"/grp/remove?id="+id};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
        } else {
            this.grps.splice(i,1);
        }
    });
},
update_grp() {
    var g=this.edtGrp;
    var dta={id:g.id,name:g.name,descr:g.descr};
    var opts={method:"PUT",url:"/grp/set",data:dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var i=this.edtGrp.i;
        this.edtGrp={dlg:false,name:'',descr:'',type:''};
        this.grps[i].name=g.name;
        this.grps[i].descr=g.descr;
    });
},
on_edit_grp(i) {
    var g=this.grps[i];
    this.edtGrp={dlg:true,id:g.id,name:g.name,descr:g.descr,i:i};
},
add_member() {
    var dta={gid:this.gid,uid:this.newMbr.uid[0],
        title:this.newMbr.title,role:this.newMbr.role};
    var opts={method:"POST",url:"/api/member/add",data:dta};
    request(opts, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query_subs();
        this.newMbr={dlg:false,uid:[],title:'',role:''};
    });
},
rmv_member(id,i) {
    var opts={method:"DELETE",url:"/api/member/remove?gid="+this.gid+"&uid="+id};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.members.splice(i,1);
    });
},
open_grp(id,name){
    if(id==this.gid){
        return;
    }
    if(id==0){
        this.paths=[];
    } else {
        for(var i in this.paths){
            if(this.paths[i].id==id){
                this.paths.length=i;//删除后面的
                break;
            }
        }
        this.paths.push({n:name, id:id});
    }
    this.gid=id;
    this.query_subs();
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.grp.title}}</q-toolbar-title>
     <div v-show="gid>0">
      <q-btn @click="newGrp.dlg=true" icon="create_new_folder" flat></q-btn>
      <q-btn @click="newMbr.dlg=true" icon="person_add" flat></q-btn>
     </div>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<q-breadcrumbs gutter="sm" class="q-pb-lg cursor-pointer text-primary">
  <q-breadcrumbs-el @click="open_grp(0,'')" icon="home"></q-breadcrumbs-el>
  <q-breadcrumbs-el v-for="p in paths" :label="p.n" @click="open_grp(p.id,p.n)"></q-breadcrumbs-el>
</q-breadcrumbs>
<q-separator color="teal"></q-separator>
<q-list>
  <q-item clickable v-for="(g,i) in grps" @click="open_grp(g.id,g.name)">
    <q-menu touch-position context-menu v-if="g.id>=100">
      <q-list dense style="min-width:100px">
        <q-item clickable v-close-popup @click="on_edit_grp(i)">
          <q-item-section avatar><q-icon name="edit" color="primary"></q-icon></q-item-section>
          <q-item-section>{{tags.modify}}</q-item-section>
        </q-item>
        <q-item clickable v-close-popup @click="rmv_grp(g.id,i)">
          <q-item-section avatar><q-icon name="delete_forever" color="red"></q-icon></q-item-section>
          <q-item-section>{{tags.remove}}</q-item-section>
        </q-item>
      </q-list>
    </q-menu>
   <q-item-section thumbnail>
    <q-icon name="folder" :color="g.type=='D'?'orange':'amber'"></q-icon>
   </q-item-section>
   <q-item-section>{{g.name}}</q-item-section>
   <q-item-section>{{g.descr}}</q-item-section>
   <q-item-section>{{g.createAt}}</q-item-section>
  </q-item>
  <q-item v-for="(m,i) in members">
    <q-menu touch-position context-menu>
     <q-list dense style="min-width:100px">
      <q-item clickable v-close-popup @click="rmv_member(m.uid,i)">
        <q-item-section avatar><q-icon name="delete_forever" color="red"></q-icon></q-item-section>
        <q-item-section>{{tags.remove}}</q-item-section>
      </q-item>
     </q-list>
    </q-menu>
    <q-item-section thumbnail><q-icon name="person_outline" color="indigo"></q-icon></q-item-section>
    <q-item-section>{{m.account}}/{{m.name}}</q-item-section>
    <q-item-section>{{m.role}}/{{m.title}}</q-item-section>
    <q-item-section>{{m.createAt}}</q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="newMbr.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
      <div class="text-h6">{{tags.grp.addMbr}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
    <user-selector :label="tags.grp.account"
      :accounts="newMbr.uid" :multi="false" useid="true"></user-selector>
    <q-select v-model="newMbr.role" :options="roleOpts"
     :label="tags.grp.role" dense map-options emit-value></q-select>
    <q-input :label="tags.grp.mbrTitle" v-model="newMbr.title" dense></q-input>
  </q-card-section>
  <q-card-actions align="right">
     <q-btn :label="tags.ok" color="primary" @click="add_member"></q-btn>
     <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="newGrp.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.add}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none"><div class="q-pa-sm">
    <q-input :label="tags.grp.name" v-model="newGrp.name" dense></q-input>
    <div class="q-gutter-sm">
     <q-radio v-model="newGrp.type" class="text-caption"
      v-for="(s,v) in tags.grpTp" :val="v" :label="s"></q-radio>
    </div>
    <q-input :label="tags.grp.descr" v-model="newGrp.descr" dense></q-input>
  </div></q-card-section>
  <q-card-actions align="right">
     <q-btn :label="tags.ok" color="primary" @click="create_grp"></q-btn>
     <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="edtGrp.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.editGrp}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-list dense>
    <q-item><q-item-section>
      <q-input v-model="edtGrp.name" :label="tags.grp.name" dense></q-input>
    </q-item-section></q-item>
    <q-item><q-item-section>
      <q-input v-model="edtGrp.descr" :label="tags.grp.name" dense></q-input>
    </q-item-section></q-item>
   </q-list>
  </q-card-section>
  <q-card-actions align="right">
     <q-btn :label="tags.ok" color="primary" @click="update_grp"></q-btn>
     <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}