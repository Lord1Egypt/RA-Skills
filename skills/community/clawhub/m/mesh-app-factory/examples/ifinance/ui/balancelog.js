const EMPTY_LOG={type:'',expireAt_s:'',val:'',forEver:false};
export default {
inject:['service', 'tags'],
data() {return {
    list:[],
    types:[],
    ctrl:{cur:1,max:0,addDlg:false,updDlg:false,dta:{},opts:[],no:-1}
}},
created(){
    var types={};
    var opts=[];
    for(var cls in this.tags.balTypes) {
        var tps=this.tags.balTypes[cls].types;
        for(var t in tps) {
            types[t]=tps[t];
            opts.push({label:tps[t], value:t});
        }
    }
    this.ctrl.opts=opts;
    this.types=types;
    this.query(1);
},
methods:{
query(pg){
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var opts={method:"GET", url:"/balance/logs?offset="+offset+"&num="+this.service.N_PAGE};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.list=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        
        var dt=new Date();
        var cur=dt.getTime();
        this.list=resp.data.list.map(b=>{
            dt.setTime(b.createAt*60000);
            b.createAt=datetime2str(dt);
            b.type=this.types[b.type];
            if(b.expireAt==MAX_INT) {
                b.expireAt_s=this.tags.forEver;
                b.forEver=true;
            } else {
                dt.setTime(b.expireAt*60000);
                b.expireAt_s=datetime2str(dt);
                b.forEver=false;
                if(cur>=dt.getTime()) {
                    b.expireAt_s += ' ' + this.tags.expired;
                    if(b.deducted=='Y') { //没过期的无法扣减
                        b.expireAt_s += ' ' + this.tags.balLog.deducted;
                    }
                }
            }
            return b;
        });
        this.ctrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
show_dtl(i) {
    if(i>-1) {
        copyObjTo(this.list[i], this.ctrl.dta);
        this.ctrl.dta.cur=parseInt((new Date()).getTime()/60000); //当前时间
        this.ctrl.updDlg=true;
    } else {
        copyObjTo(EMPTY_LOG, this.ctrl.dta);
        this.ctrl.addDlg=true;
    }
    this.ctrl.no=i;
},
add() {
    if(this.ctrl.dta.forEver) {
        this.ctrl.dta.expireAt=MAX_INT;
    } else {
        this.ctrl.dta.expireAt=parseInt(Date.parse(this.ctrl.dta.expireAt_s)/60000);
    }
    var dta=copyObj(this.ctrl.dta,['id','expireAt','cmt','val','type']);
    var opts={method:"POST",url:"/balance/add",data:dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query(this.ctrl.cur);
        this.ctrl.addDlg=false;
    })
},
update() {
    if(this.ctrl.no<0)return;
    if(this.ctrl.dta.forEver) {
        this.ctrl.dta.expireAt=MAX_INT;
    } else {
        this.ctrl.dta.expireAt=parseInt(Date.parse(this.ctrl.dta.expireAt_s)/60000);
    }
    var dta=copyObj(this.ctrl.dta,['id','expireAt','cmt']);
    var opts={method:"PUT",url:"/balance/update",data:dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query(this.ctrl.cur);
        this.ctrl.updDlg=false;
    })
},
remove() {
    if(this.ctrl.no<0)return;
    var d=this.ctrl.dta;
    var opts={method:"DELETE",url:"/balance/remove?id="+d.id};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query(this.ctrl.cur);
        this.ctrl.updDlg=false;
        this.ctrl.no=-1;
    })
},
deduct() {
    if(this.ctrl.no<0)return;
    var d=this.ctrl.dta;
    var opts={method:"DELETE",url:"/balance/deduct?id="+d.id};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query(this.ctrl.cur);
        this.ctrl.updDlg=false;
        this.ctrl.no=-1;
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.balLog.title}}</q-toolbar-title>
     <q-btn flat icon="add" dense @click="ctrl.addDlg=true"></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-show="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-list separator>
 <q-item>
  <q-item-section><q-item-label caption>{{tags.balLog.createAt}}/{{tags.balLog.expireAt}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.balLog.type}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.cmt}}</q-item-label></q-item-section>
  <q-item-section side><q-item-label caption>{{tags.balLog.val}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="(b,i) in list" clickable @click="show_dtl(i)">
  <q-item-section>
   <q-item-label>{{b.createAt}}</q-item-label>
   <q-item-label caption>{{b.expireAt_s}}</q-item-label>
  </q-item-section>
  <q-item-section>{{b.type}}</q-item-section>
  <q-item-section>{{b.cmt}}</q-item-section>
  <q-item-section side>{{b.val}}</q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.addDlg">
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{tags.add}}</div>
  </q-card-section>
  <q-card-section class="q-pt-sm">
   <q-select v-model="ctrl.dta.type" :label="tags.balLog.type"
    :options="ctrl.opts" emit-value  map-options></q-select>
   <q-input :label="tags.balLog.val" v-model.number="ctrl.dta.val" dense type="number"></q-input>

   <q-checkbox :label="tags.forEver" v-model="ctrl.dta.forEver"></q-checkbox>
   <date-input :label="tags.balLog.expireAt" v-model="ctrl.dta.expireAt_s" :disable="ctrl.dta.forEver"></date-input>
   <q-input :label="tags.cmt" v-model="ctrl.dta.cmt" dense></q-input>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn :label="tags.ok" color="primary" @click="add"></q-btn>
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="ctrl.updDlg">
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{tags.modify}}</div>
  </q-card-section>
  <q-card-section class="q-pt-sm">
   <div>{{ctrl.dta.type}}</div>
   <div>{{ctrl.dta.val}}</div>
   <q-checkbox :label="tags.forEver" v-model="ctrl.dta.forEver" dense></q-checkbox>
   <date-input :label="tags.balLog.expireAt" v-model="ctrl.dta.expireAt_s" :disable="ctrl.dta.forEver" min="today"></date-input>
   <q-input :label="tags.cmt" v-model="ctrl.dta.cmt" dense></q-input>
  </q-card-section>
  <q-card-actions class="row">
   <div class="col text-left" v-if="ctrl.dta.deduct=='N'">
    <q-btn :label="tags.remove" color="red" @click="remove" flat></q-btn>
    <q-btn :label="tags.deduct" color="red" @click="deduct" flat
     v-if="ctrl.dta.expireAt<ctrl.dta.cur"></q-btn>
   </div>
   <div class="col text-right">
    <q-btn :label="tags.ok" color="primary" @click="update"></q-btn>
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
   </div>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}