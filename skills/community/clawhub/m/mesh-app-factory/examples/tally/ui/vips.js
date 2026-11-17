const EMPTY_VIP={name:'',mobile:'',sex:'',birth:'',code:''}
export default {
inject:['service', 'tags'],
data() {return {
    role:'',
    score:{total:0,vip:0},
    vips:[], //会员列表
    search:'',
    ctrl:{cur:1,max:0,searchTag:''},
    newVip:{dlg:false}
}},
created(){
    var cur=this.service.getRt("cur", 1);
    this.ctrl.cur=cur;
    this.isOwner=this.service.getRole().then(role=>{
        this.role=role;
        this.query_vips(cur);
    })
},
methods:{
query_vips(pg) {
    var offset=(parseInt(pg)-1)*this.service.NUM_PER_PAGE;
    this.service.setRt("cur", pg);
    this.search="";
    
    var url=this.role=='admin'?"/vip/list":"/vip/my";
    url+="?offset="+offset+"&num="+this.service.NUM_PER_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.vips=[];
            this.ctrl.max=0;
            this.ctrl.searchTag=this.tags.search;
        } else {
            this.score.total=resp.data.total;
            this.score.vip=resp.data.vip;
            this.score.nOrder=resp.data.nOrder;
            this.score.nService=resp.data.nService;
            this.formatData(resp.data.list, resp.data.cols);
            this.ctrl.max=Math.ceil(resp.data.total/this.service.NUM_PER_PAGE);
            this.ctrl.searchTag=this.tags.search + '(' + resp.data.total + ')';
        }
    })
},
refresh() {
    this.query_vips(this.ctrl.cur);
},
search_vips() {
    if(this.search=='') {
        this.query_vips(1);
        return;
    }
    var url="/api/vip/search?s="+this.search+"&limit="+this.service.NUM_PER_PAGE
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.formatData(resp.data.list, resp.data.cols);
        this.ctrl.max=1;
    })
},
formatData(rows,cols) {
    var dt=new Date();
    var nowYear = dt.getFullYear();
    this.vips=rows.map(l=>{
        var r={};
        for(var i in cols) {
            r[cols[i]]=l[i];
        }
        dt.setTime(r.createAt*60000);
        r.createAt = datetime2str(dt);
        dt.setTime(r.birth*86400000);
        r.birth = date2str(dt);
        r.age=nowYear-dt.getFullYear();
        r.sex=this.tags.sexInfo[r.sex].n;
        return r;
    })
},
add_vip() {
    var url="/api/vip/add";
    var d=this.newVip;
    var birth=Math.round(new Date(this.newVip.birth).getTime()/86400000);
    var reqDta=copyObj(this.newVip);
    reqDta.birth=birth;
    request({method:"POST",url:url,data:reqDta}, this.service.name).then(resp => {
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.newVip.dlg=false;
        this.query_vips(1);
    })
},
open_newvip_dlg() {
    copyObjTo(EMPTY_VIP, this.newVip);
    this.newVip.dlg=true;
},
showBrokerage() {
    if(this.role=='admin') {
        this.service.goto('/brokerages')
    } else {
        this.service.goto('/mybrokerage')
    }
}
},

template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary">
   <q-toolbar>
    <q-avatar square><img src="./favicon.png"></q-avatar>
    <q-toolbar-title>{{tags.app_name}}</q-toolbar-title>
    <q-btn icon="refresh" flat dense @click="refresh"></q-btn>
    <q-btn flat dense icon="menu" v-if="role=='admin'">
    <q-menu>
     <q-list class="text-primary">
      <q-item clickable @click="service.goto('/settings')" v-if="service.account=='admin'">
       <q-item-section avatar><q-icon name="settings"></q-icon></q-item-section>
       <q-item-section>{{tags.settings}}</q-item-section>
      </q-item>
      <q-item clickable @click="service.goto('/reports')">
       <q-item-section avatar><q-icon name="bar_chart"></q-icon></q-item-section>
       <q-item-section>{{tags.report.title}}</q-item-section>
      </q-item>
     </q-list>
    </q-menu>
    </q-btn>
   </q-toolbar>
   <q-card class="text-white q-mx-sm bg-indigo-8" flat>
    <q-card-action>
    <q-markup-table flat dark dense style="background:radial-gradient(circle,#33a2ff 0%,#014aaa 100%)">
     <tr>
      <th>{{tags.score.total}}</th>
      <th>{{tags.score.vip}}</th>
      <th>{{tags.score.nOrder}}</th>
      <th>{{tags.score.nService}}</th>
     </tr>
     <tr>
      <td class="text-h6 text-center">{{score.total}}</td>
      <td class="text-h6 text-center">{{score.vip}}</td>
      <td class="text-h6 text-center">{{score.nOrder}}</td>
      <td class="text-h6 text-center">{{score.nService}}</td>
     </tr>
    </q-markup-table>
    </q-card-action>
    <q-card-actions align="right">
     <q-btn @click="showBrokerage" :label="tags.brokerage.title"
      icon="score" flat dense v-if="role=='admin'"></q-btn>
     <q-btn @click="service.goto('/orders')" :label="tags.order.title"
      icon="monetization_on" flat dense></q-btn>      
     <q-btn @click="service.goto('/services')" :label="tags.service.title"
      icon="group" flat dense></q-btn>
     <q-btn @click="service.goto('/mytasks')" :label="tags.service.myTask"
      icon="assignment" flat dense></q-btn>
    </q-card-actions>
   </q-card>
  </q-header>
  <q-footer class="bg-white q-pa-md">
    <q-input outlined v-model="search" :label="ctrl.searchTag" dense @keyup.enter="search_vips">
    <template v-slot:append>
      <q-icon name="close" v-show="search!==''" @click="query_vips(1)" class="cursor-pointer q-mr-md"></q-icon>
      <q-icon name="search" @click="search_vips" class="cursor-pointer q-mr-md"></q-icon>
    </template>
    <template v-slot:after>
      <q-btn round color="primary" icon="add_circle" @click="open_newvip_dlg"></q-btn>
    </template>
    </q-input>
  </q-footer>

  <q-page-container>
    <q-page class="q-pa-md">

<div class="q-pa-sm flex flex-center" v-if="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_vips"></q-pagination>
</div>
<q-markup-table flat>
 <thead><tr>
  <th class="text-left">{{tags.vip.name}}</th>
  <th class="text-left">{{tags.vip.code}}</th>
  <th class="text-right">{{tags.createAt}}</th>
 </tr></thead>
 <tbody>
 <tr v-for="v in vips" @click="service.goto('/vip?id='+v.id)" style="cursor:pointer;">
  <td class="text-left">
    <div>{{v.name}}({{v.sex}}, {{v.age}})</div>
    <div class="text-caption">{{tags.birth}}:{{v.birth}}</div>
  </td>
  <td class="text-right">
   <div>{{v.code}}</div>
   <div class="text-caption">{{v.cmt}}</div>
  </td>
  <td class="text-right">{{v.createAt}}</td>
 </tr>
 </tbody>
</q-markup-table>
    </q-page>
  </q-page-container>
</q-layout>
    
<q-dialog v-model="newVip.dlg">
  <q-card style="min-width:70vw" class="q-pa-md">
    <q-card-section>
     <div class="text-h6">{{tags.addVip}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-input v-model="newVip.name" :label="tags.vip.name" dense
     :rules="[v=>v!=''|| tags.namePls]"></q-input>
     <div class="q-gutter-sm">
      <q-radio v-model="newVip.sex" val="M" :label="tags.sexInfo.M.n"></q-radio>
      <q-radio v-model="newVip.sex" val="F" :label="tags.sexInfo.F.n"></q-radio>
      <q-radio v-model="newVip.sex" val="U" :label="tags.sexInfo.U.n"></q-radio>
     </div>
     <q-input v-model="newVip.code" :label="tags.vip.code" dense></q-input>
     <q-input v-model="newVip.mobile" :label="tags.mobile" maxlength=11
     :rules="[v=>/^1[0-9]{10}$/.test(v)|| tags.mobilePls]" dense></q-input>
      <component-date-input :close="tags.ok" :label="tags.birth" v-model="newVip.birth" max="today"></component-date-input>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
      <q-btn :label="tags.ok" color="primary" @click="add_vip"></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
`
}